import json
import logging

from aiohttp.client import ClientSession

from pylnbits.utils import delete_url, get_url, post_url

"""
Rest API methods for LNbits User Manager Extension

GET users
GET user (single user)
GET wallets
GET transactions
POST wallet
POST user + initial wallet - add email and password fields! - todo + test

DELETE user and their wallets
DELETE wallet
POST activate extension
"""

###################################
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logging.getLogger("pylnbits").setLevel(level=logging.WARNING)
logger = logging.getLogger(__name__)
###################################


class UserManager:
    def __init__(self, config, session: ClientSession = None):
        self._config = config
        self._lnbits_url = config.lnbits_url
        self._invoice_headers = config.invoice_headers()
        self._admin_headers = config.admin_headers()
        self._session = session

    # returns JSON list of users
    async def get_users(self):
        try:
            upath = "/usermanager/api/v1/users"
            path = self._lnbits_url + upath
            res = await get_url(session=self._session, path=path, headers=self._invoice_headers)
            return res
        except Exception as e:
            logger.info(e)
            return e

    # returns single JSON user based on user_id
    async def get_user(self, user_id):
        try:
            upath = "/usermanager/api/v1/users/" + user_id
            path = self._lnbits_url + upath
            res = await get_url(session=self._session, path=path, headers=self._invoice_headers)
            return res
        except Exception as e:
            logger.info(e)
            return e

    # returns JSON wallet data
    async def get_wallets(self, user_id):
        try:
            wpath = "/usermanager/api/v1/wallets/" + user_id
            path = self._lnbits_url + wpath
            res = await get_url(session=self._session, path=path, headers=self._invoice_headers)
            return res
        except Exception as e:
            logger.info(e)
            return e

    # returns JSON of wallet transactions
    async def get_tx(self, wallet_id):
        try:
            tpath = "/usermanager/api/v1/wallets" + wallet_id
            path = self._lnbits_url + tpath
            res = await get_url(session=self._session, path=path, headers=self._invoice_headers)
            return res
        except Exception as e:
            logger.info(e)
            return e

    # creates a user and initial wallet
    # TODO add  email and password optional
    # {"admin_id": <string>, "user_name": <string>, "wallet_name": <string>,
    # "email": <Optional string> ,"password": <Optional string>}
    async def post_user_initial(self, admin_id, user_name, wallet_name):

        try:
            tpath = "/usermanager/api/v1/users"
            path = self._lnbits_url + tpath
            body = {"admin_id": admin_id, "user_name": user_name, "wallet_name": wallet_name}
            jbody = json.dumps(body)
            res = await post_url(session=self._session, path=path, headers=self._invoice_headers, body=jbody)
            return res
        except Exception as e:
            logger.info(e)
            return e

    # body = {"user_id": <string>, "wallet_name": <string>, "admin_id": <string>}
    # returns 201 CREATED
    # {"id": <string>, "admin": <string>, "name": <string>,
    # "user": <string>, "adminkey": <string>, "inkey": <string>}
    async def post_wallet(self, user_id, wallet_name, admin_id):
        try:
            tpath = "/usermanager/api/v1/wallets"
            path = self._lnbits_url + tpath
            body = {"user_id": user_id, "wallet_name": wallet_name, "admin_id": admin_id}
            jbody = json.dumps(body)
            res = await post_url(session=self._session, path=path, headers=self._invoice_headers, body=jbody)
            return res
        except Exception as e:
            logger.info(e)
            return e

    async def delete_user(self, user_id):
        try:
            tpath = "/usermanager/api/v1/users/" + user_id
            path = self._lnbits_url + tpath
            res = await delete_url(session=self._session, path=path, headers=self._invoice_headers)
            return res
        except Exception as e:
            logger.info(e)
            return e

    async def delete_wallet(self, wallet_id):
        try:
            tpath = "/usermanager/api/v1/wallets/" + wallet_id
            path = self._lnbits_url + tpath
            res = await delete_url(session=self._session, path=path, headers=self._invoice_headers)
            return res
        except Exception as e:
            logger.info(e)
            return e

    # temporarily use this to activate extensions:
    # https://yourdomain.com/extensions?usr=89.....&enable=lnurlp
    # unclear why curl doesn't work ?
    async def post_activate_ext(self, user_id: str, extension: str, active: int):
        try:
            tpath = "/usermanager/api/v1/extensions"
            path = self._lnbits_url + tpath
            body = {"userid": user_id, "extension": extension, "active": active}
            jbody = json.dumps(body)
            res = await post_url(session=self._session, path=path, headers=self._invoice_headers, body=jbody)
            return res
        except Exception as e:
            logger.info(e)
            return e
