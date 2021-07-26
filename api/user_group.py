'''
User group API
'''
from flask_restx import Resource

from data.group import get_all_groups
from models.user import User, UserRole
from lookup.user_group import UserGroupLookup, ADMINISTRATOR_KEY
from core import Namespace


api = Namespace('user permission groups', description='Get group of users in each group')

@api.route('/get/<string:group_path>/')
@api.param('group_path', 'Group path string or "Administrator"')
class UserGroupAPI(Resource):
    '''
    User group API
    '''
    def get(self, group_path):
        '''
        Get users from group path
        '''
        lookup = UserGroupLookup()
        user_ids = lookup.table[group_path]
        users = [User.get(user_id) for user_id in user_ids]
        return [user.dict() for user in users]

@api.route('/add/')
class UserGroupAddAPI(Resource):
    '''
    Add user group API
    '''
    def post(self):
        '''
        Add user to group
        body {
            email: string,
            group: string,
        }
        '''
        email = api.payload['email']
        group = api.payload['group']
        UserGroupController.add_user_to_group(email, group)

@api.route('/remove/')
class UserGroupRemoveAPI(Resource):
    '''
    Remove user group API
    '''
    def post(self):
        '''
        Remove user from group
        body {
            userid: string,
            group: string,
        }
        '''
        userid = api.payload['userid']
        group = api.payload['group']
        UserGroupController.remove_user_from_group(userid, group)

class UserGroupController():
    '''
    User group controller
    '''
    @staticmethod
    def add_user_to_group(email, group):
        '''
        Add user to group
        '''
        lookup = UserGroupLookup()
        if group in lookup.table:
            user = User.query_one({'email': email})
            target_role = UserRole.ADMIN if group == ADMINISTRATOR_KEY else UserRole.VALIDATOR
            if not user:
                user = User({
                    'email': email,
                    'role': target_role.value,
                    'groups': [],
                }).save()
            else:
                if user.role == UserRole.ADMIN and group != ADMINISTRATOR_KEY:
                    raise Exception(
                        'cannot add admin to validator group. please remove this user from admin' \
                        ' role.'
                    )

            if target_role == UserRole.ADMIN:
                user.groups = get_all_groups()
            elif target_role == UserRole.VALIDATOR:
                if group not in user.groups:
                    user.groups.append(group)
            user.role = target_role
            user.save()
            lookup.add_user_to_group(user.id, group)
        else:
            raise Exception('group is not in table')

    @staticmethod
    def remove_user_from_group(user_id, group):
        '''
        Remove user from group
        '''
        lookup = UserGroupLookup()
        if group in lookup.table:
            user = User.get(user_id)
            if user:
                if group == ADMINISTRATOR_KEY:
                    user.role = UserRole.USER
                    user.groups = []
                    user.save()
                else:
                    if group in user.groups:
                        user.groups.remove(group)
                        user.save()
                lookup.remove_user_from_group(user.id, group)
