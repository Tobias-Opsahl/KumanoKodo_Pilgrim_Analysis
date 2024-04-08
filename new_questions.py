import warnings

new_questions = [
    "Reflect on life",
    "Obtain a deeper connection in life",
    "Opportunity for self-discovery",
    "Get in touch with my true self",  # NOTE: SIC from "Get in touch with true self"
    "Find inspiration in natural surroundings",  # Dropped, but commented
    "Chance to think/solve problems",
    "Stimulate creativity",
    # NOTE: SIC from "Develop a sense of self confidence"
    "Develop a sense of self-confidence",
    "Recreate in a primitive environment",  # Dropped
    "Observe and appreciate the ecosystem",
    "Explore the natural environment",
    "Experience nature's magic and mysticism",  # Dropped
    "Develop a oneness with nature",  # Dropped
    "Experience the scenic quality of nature",
    "Feel connected to a place that is important",  # Dropped
    "Being alone/solitude",
    "Free from observation from all other people",
    "Get away from daily routines",  # Dropped
    "Tranquility and peace",  # Dropped, but commented
    "Simplify daily priorities",  # Dropped
    "Physical health and exercise",  # NOTE: SIC from "Physical health/and exercise"
    # NOTE: SIC from "Feel a special closeness with others in my group"
    "Experience a sense of community with other pilgrims",
    "Be in a small intimate group",  # NOTE: SIC from "A small intimate group"
    # NOTE: SIC from "Feel a connection with others who value wilderness"
    "Feel a connection with others who value wilderness and remote places",
    "Having a sense of discovery",  # Dropped
    "Having an adventure",  # Dropped, but kind-of commented

    # The following was added by the SOW article
    "Physical challenge",
    "Develop my religious values",
    "Meet local non-pilgrims along the route",
    "Have a story to tell",  # Dropped
    "Religious experiences",
    "Experience places that I have read or been told about",
    "The religious heritage of the trail",
    # NOTE: Changed from "Visit churches or other religious buildings"
    "Visit shrines or other religious buildings",
    "Travel in a slow pace",  # NOTE: SIC from "Travel in slow pace"
    # NOTE: Changed from "Reach the holy shrine of St. Olav", Dropped, but commented
    "Reach the holy shrines of Kumano Kodo (Hongu, Shingu or Nachi)",
    "Getting to know with foreign places and landscapes",  # Dropped, but commented
    "Travel in an environment-friendly way",
    "Spiritual experiences",  # Dropped
    "Buying/consuming local products (like foods or crafts)",
    "Visit local communities",
    "The ancient heritage of the trail",  # NOTE: Changed from "The medieval heritage of the trail"
    # NOTE: Changed from "Heritage sites along the trail (churches, old farm-buildings, burial mounds etc.)"
    "Heritage sites along the trail (shrines, temples, historical landmarks, etc.)",
    "Develop my spiritual values",
    "Meditative experiences",
    "Be in the present",
    "Follow the rhythms of nature and landscape",
    "Feel free to take my time",
    "Discover my inner time",
]

factor_grouping = {
    "1 The inner me": [
        "Opportunity for self-discovery",
        "Get in touch with my true self",
        "Reflect on life",
        "Obtain a deeper connection in life",
        "Develop a sense of self-confidence",
        "Discover my inner time",
        "Chance to think/solve problems",
        "Meditative experiences",  # NOTE: SIC from "Meditative experience"
        "Develop my spiritual values",
        "Stimulate creativity",
        "Be in the present"],
    "2 The religious me": [
        "Develop my religious values",
        "Religious experiences",
        "The religious heritage of the trail",
        "Visit shrines or other religious buildings",
        "Develop my spiritual values",
        "Heritage sites along the trail (shrines, temples, historical landmarks, etc.)"],
    "3 Meet the locales and local heritage": [
        "Visit local communities",
        "The ancient heritage of the trail",
        # NOTE: SIC from "Experience places I have read or been told about"
        "Experience places that I have read or been told about",
        # NOTE: SIC from "Buying/consuming local products (like food or crafts)"
        "Buying/consuming local products (like foods or crafts)",
        "Heritage sites along the trail (shrines, temples, historical landmarks, etc.)",
        "Meet local non-pilgrims along the route"],  # NOTE: SIC from "Meet local, non-pilgrims along the route"
    "4 Slow travel": [
        "Travel in a slow pace",
        "Feel free to take my time",
        "Follow the rhythms of nature and landscape",
        "Discover my inner time",
        "Be in the present"],
    "5 Nature - knowledge and joy": [
        "Explore the natural environment",
        "Observe and appreciate the ecosystem",
        "Travel in an environment-friendly way",
        "Experience the scenic quality of nature",  # NOTE: SIC from "Enjoy the scenic quality of nature"
        "Follow the rhythms of nature and landscape"],
    "6 Exercise in nature": [
        "Physical health and exercise",
        "Physical challenge",
        "Experience the scenic quality of nature"],  # NOTE: SIC from "Enjoy the scenic quality of nature",
    "7 Hiking together": [
        "Be in a small intimate group",
        # NOTE: SIC from "Feel a connection with others who values remote places",
        "Feel a connection with others who value wilderness and remote places",
        "Experience a sense of community with other pilgrims"],
    "8 Be in solitude": [
        "Free from observation from all other people",
        "Being alone/solitude"]  # NOTE: SIC From "Be alone/solitude"
}

original_questions_to_ids = {
    new_questions[i]: i for i in range(len(new_questions))}
new_questions_to_group_id = {}
question_id_to_group_id = {}

for question in new_questions:
    group = []
    for factor, questions in factor_grouping.items():
        if question in questions:
            group.append(int(factor[0]))
    if group is None:
        print(question)
    new_questions_to_group_id[question] = group
    question_id_to_group_id[original_questions_to_ids[question]] = group


check = True
if check:
    n_questions = len(new_questions)
    n_included = n_questions - 14
    n_repeated = 0
    n_none = 0
    for group_ids in question_id_to_group_id.values():
        if len(group_ids) >= 2:
            n_repeated += len(group_ids) - 1
        if len(group_ids) == 0:
            n_none += 1

    n_total = 0
    n_missing = 0
    for group in factor_grouping:
        for question in factor_grouping[group]:
            n_total += 1
            if question not in new_questions:
                n_missing += 1
                warnings.warn(f"\n`{question}` not in `new_questions`\n")

    n_unique_in_grouping = n_total - n_missing - n_repeated
    if n_unique_in_grouping != n_included:
        message = "Unique questions in factor grouping and questions included does not match, was "
        message += f"{n_unique_in_grouping} and {n_included}"
        raise Exception(message)
