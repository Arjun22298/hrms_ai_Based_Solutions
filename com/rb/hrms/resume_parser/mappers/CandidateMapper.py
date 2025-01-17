from com.rb.hrms.resume_parser.models.CandidateDetails import CandidateDetails, Qualification, Skill, City
from com.rb.hrms.resume_parser.models.CandidateRawDetails import CandidateRawDetails


class CandidateMapper:
    @staticmethod
    def map(candidate_instance):
        candidate_details_data = {
            "fullName": candidate_instance.candidateName,
            "email": candidate_instance.email,
            "contactNo": candidate_instance.phoneNumber,
            "altContactNo": candidate_instance.cleanedAltContactNo,
            "gender": candidate_instance.gender,
            "birthDate": candidate_instance.dateOfBirth,
            "passingYear": candidate_instance.passingYear,
            "whatsappNo": None,
            "resumeUrl": candidate_instance.processedDataFolder,
            "linkedInUrl": candidate_instance.linkedUrl,
            "experienceInYears": candidate_instance.totalNumberOfYearExperience,
            "profileScannedOn": candidate_instance.processDate,
            "currentCompanyName": candidate_instance.currentCompanyName,
            "profileReferance": None,  # Set a default value or handle differently based on your needs
            "feedbackStatus": None,  # Set a default value or handle differently based on your needs
            "address": candidate_instance.address,
            "qualification": {
                "id": candidate_instance.cleanedQualificationId.get('id'),
                "name": candidate_instance.cleanedQualificationId.get('name'),
                "description": candidate_instance.cleanedQualificationId.get('description'),
                "isActive": candidate_instance.cleanedQualificationId.get('isActive')
            },
            "city": {
                "id": candidate_instance.cleanedCityId.get('id'),
                "cityName": candidate_instance.cleanedCityId.get('cityName'),
                "isActive": candidate_instance.cleanedCityId.get('isActive')
            },
            "skills": candidate_instance.skills,  # Handle differently based on your needs
            "statusId": {
                "id": 1,
                "statusName": "Active",
                "statusType": "Custom Statuses",
                "isActive": "true"
            }
        }
        return candidate_details_data

        # return CandidateDetails(**candidate_details_data)
