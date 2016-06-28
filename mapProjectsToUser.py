from user_features import getUserVector
from project_features import getProjectVector
from chatbot import get_cosine


def sortProjects(projects, user):
	userVec= getUserVector(user)
	cosine_list = []
	for project in projects:
		projectVec= getProjectVector(project)
		cos = get_cosine(userVec, projectVec)
		cosine_list.append([cos, project])
	cosine_list.sort()
	return [j for i,j in cosine_list]
