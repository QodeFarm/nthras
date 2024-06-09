from drf_yasg.generators import OpenAPISchemaGenerator

class CustomOpenAPISchemaGenerator(OpenAPISchemaGenerator):
    def get_paths_object(self, paths):
        paths = super().get_paths_object(paths)
        # print("Available paths:", paths.keys())
        paths.pop('/users/create_user/reset_password/', None)
        paths.pop('/users/create_user/resend_activation/', None)
        paths.pop('/users/create_user/me/', None)
        paths.pop('/users/create_user/activation/', None)
        paths.pop('/users/create_user/set_password/', None)
        paths.pop('/users/create_user/reset_password_confirm/', None)
        paths.pop('/users/create_user/reset_username_confirm/', None)
        paths.pop('/users/create_user/reset_username/', None)
        paths.pop('/users/create_user/set_username/', None)
        paths.pop('/users/create_user/{user_id}/', None)
        return paths

