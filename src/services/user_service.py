from src.dtos.user_dtos import UserIncomingDto
def get_temp_user() -> UserIncomingDto: 
    """
    Gets a usable user dto, should be replaced with a MS Graph service that gets the user information
    """
    return UserIncomingDto(id=None, azure_id="c35fd60c-60db-4fa6-891b-8edec06865f9", name="John Doe")