import math
from sklearn.cluster import KMeans
from sqlalchemy import func
from src.services.db_service import db


def expected_prob(Rs, Rq, scale=400.0):
    return 1.0 / (1.0 + 10.0 ** ((Rq - Rs) / scale))

# after each question is answered, update student elo
# Rs = student rating, Rq= question rating, correct = student input
# output = return student elo ranking after question 
def update_student(Rs, Rq, correct: bool, K=24.0, scale=400.0):
    p = expected_prob(Rs, Rq, scale=scale)
    S = 1.0 if correct else 0.0
    return Rs + K * (S - p)

# gets the teacher id then returns a dictinary conating the student id, their average elo, their cluster id, and their cluster label
def compute_student_clusters(teacher_id):

    student_ids = db.session.execute(db.text("SELECT student_id FROM teachers_students WHERE teacher_id =:id"), {"id": teacher_id}).scalars().all()
    if not student_ids:
        return []

    avg_elos = []
    student_list = []
    student_assignments = []

    for sid in student_ids:
        result = db.session.execute(
            db.text("""
                SELECT AVG(rating) AS avg_elo
                FROM elo
                WHERE user_id = :sid
            """),
            {"sid": sid}
        ).mappings().fetchone()

        if result['avg_elo'] is None:
            student_assignments.append({
            "student_id": sid,
            "avg_elo": None,
            "cluster_id": None,
            "cluster_label": "No information"
            })
            continue


        avg_elo = float(result["avg_elo"])
        avg_elos.append(avg_elo)
        student_list.append((sid, avg_elo))

    # If no students have ELO data, return early with just the "No information" students
    if not avg_elos:
        student_assignments.sort(key=lambda x: x["student_id"])
        return student_assignments

    X = [[elo] for elo in avg_elos]

    num_clusters = min(4, len(avg_elos))
    kmeans = KMeans(n_clusters=num_clusters, random_state=42, n_init=10)
    labels = kmeans.fit_predict(X)

    cluster_means = {}
    for c in range(num_clusters):
        values = [avg_elos[i] for i in range(len(avg_elos)) if labels[i] == c]
        cluster_means[c] = sum(values) / len(values) if values else 0

    sorted_clusters = sorted(cluster_means, key=lambda c: cluster_means[c])
    skill_labels = ["Beginner", "Intermediate", "Advanced", "Expert"]

    cluster_to_label = {
        sorted_clusters[i]: skill_labels[i]
        for i in range(num_clusters)
    }

    
    for i, (sid, elo) in enumerate(student_list):
        cid = labels[i]
        label = cluster_to_label[cid]

        student_assignments.append({
            "student_id": sid,
            "avg_elo": elo,
            "cluster_id": cid,
            "cluster_label": label
        })


    cluster_ranges = {}
    for cid in range(num_clusters):
        label_name = cluster_to_label[cid]
        values = [avg_elos[i] for i in range(len(avg_elos)) if labels[i] == cid]
        if not values:
            continue

        cluster_ranges[label_name] = {
            "min": min(values),
            "max": max(values),
            "mean": cluster_means[cid]
        }

    # sorts the students in asending order
    student_assignments.sort(key=lambda x: x["student_id"])

    return student_assignments
#algorithm for elo quiz creation and ml training
ANCHORS = {"easy": 900, "medium": 1000, "hard": 1100}


def difficulty_weights(student_elo: float, spread: float = 90.0):
    raw = {k: math.exp(-((student_elo - rq) ** 2) / (2 * spread ** 2)) for k, rq in ANCHORS.items()}
    total = sum(raw.values())
    return {k: raw[k] / total for k in raw}


def _alloc(weights: dict, quiz_len: int):
    floats = {k: weights[k] * quiz_len for k in weights}
    floors = {k: int(floats[k]) for k in floats}
    leftover = quiz_len - sum(floors.values())


    remainders = sorted(((floats[k] - floors[k], k) for k in floors), reverse=True)
    for _, k in remainders[:leftover]:
        floors[k] += 1
    return floors


def mix_for_next_quiz(student_elo: float, quiz_len: int, spread: float = 90.0):
    return _alloc(difficulty_weights(student_elo, spread), quiz_len)
