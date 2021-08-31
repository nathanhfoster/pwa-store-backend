import requests
import html
from bs4 import BeautifulSoup
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions, status
from pwa_store_backend.users.models import User
import re

manifest_regex = r"\/manifest.([^&]*)"

class PwaInfoView(APIView):
    """
      parse the index page to get the manifest json from the link
    """
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_manifest(self, url):
        r = requests.get(url, timeout=8)
        json_response = r.json()
   
        final_response = {
          "manifest_url": url,
          "manifest_json": json_response,
        }
        return Response(final_response, status=status.HTTP_200_OK)

    def get(self, request, format=None):
        url = request.query_params.get('url')
        try:
            return self.get_manifest(url if re.search(manifest_regex, url) else F"{url}/manifest.json")
        except Exception as e:
            print("Error", e)

        try:
            r = requests.get(url)
            page = html.unescape(r.text)
            soup = BeautifulSoup(page)
            manifest_url = soup.find("link", { "rel":"manifest" })['href']
            if 'http' in manifest_url:
                return self.get_manifest(manifest_url)
            else:
                return self.get_manifest(F"{url}manifest_url")
        except Exception as e:
            return Response({"error": "Invalid URL"}, status=status.HTTP_406_NOT_ACCEPTABLE)
