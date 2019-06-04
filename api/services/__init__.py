# import abc
#
#
# class EglService:
#     __metaclass__ = abc.ABCMeta
#
#     def __init__(self):
#         EglServiceManager.register_service(self.__class__)
#
#
# class EglServiceManager:
#
#     instance = None
#
#     class __EglServiceManager:
#         def start_all_services(self):
#             for service in self.registered_services:
#                 service()
#
#     def __init__(self):
#         if not EglServiceManager.instance:
#             EglServiceManager.instance = EglServiceManager.__EglServiceManager()
#
#     def __getattr__(self, item):
#         getattr(self.instance, item)
#
#     def __setattr__(self, key, value):
#         setattr(self.instance, key, value)
