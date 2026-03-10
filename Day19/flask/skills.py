skills_list = [
"python",
"machine learning",
"deep learning",
"sql",
"flask",
"tensorflow",
"pandas",
"numpy",
"data analysis",
"html",
"css","javascript",
"react","aws","docker","kubernetes",
"git","github","linux","bash","c++","java",
"c","ruby","php","go","swift","r","matlab",
]

def extract_skills(text):

    found = []

    for skill in skills_list:
        if skill in text.lower():
            found.append(skill)

    return found