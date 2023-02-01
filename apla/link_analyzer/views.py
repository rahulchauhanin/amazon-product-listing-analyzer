from django.shortcuts import render
from django.views import View
import requests
from bs4 import BeautifulSoup
import re
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string

def about(request):
    return render (request, "about.html")

# Create your views here.
class LinkAnalyzerView(View):

    def get(self, request):
        return render(request, "index.html")

    def post(self, request):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
            "Accept-Encoding": "gzip, deflate",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "DNT": "1",
            "Connection": "close",
            "Upgrade-Insecure-Requests": "1",
        }

        url = request.POST.get('txt-url')
        
        # Send an HTTP request to the URL and store the response
        response = requests.get(url.strip(), headers=headers)

        # Parse the HTML content of the page
        soup = BeautifulSoup(response.content, "html.parser")

        # Find product title
        try:
            product_title = soup.find("span", attrs={"id": 'productTitle'}).string
        except AttributeError:
            product_title = ""
        
        # Rest of the processing happens, only if a valid product title is found.
        if product_title != "":

            # Find product description
            try:
                product_description = soup.find("div", attrs={"id": 'productDescription'}).findNext('span').string
            except AttributeError:
                product_description = "NA"

            # Find product images           
            product_images = 0
            try:
                for link in soup.find("div", attrs={"id": 'altImages'}).findNext('ul').find_all('img', src=re.compile(".jpg")):
                    stuff = link.get('src')
                    if '.jpg' in stuff and "play-icon-overlay" not in stuff :
                        product_images += 1
            except AttributeError:
                product_images = ""

            # Find product videos
            try:
                product_videos = soup.find("span", class_="a-size-mini a-color-secondary video-count a-text-bold a-nowrap").string
                product_videos = product_videos.replace(' VIDEOS','').replace('VIDEO','')
            except AttributeError:
                product_videos = 0
            
            # Find product features
            try:
                product_features = soup.find("div", id="feature-bullets").findNext('ul').find_all('li')
                featureslist = []
                for pf in product_features:
                    featureslist.append(pf.text)
            except AttributeError:
                featureslist = []

            # Find product ratings
            try:
                product_rating = soup.find("span", attrs={'class': 'a-icon-alt'}).string
                if product_rating == "Previous page":
                    product_rating = "NA"
                else:
                    product_rating = float(product_rating[0:3])
            except AttributeError:
                product_rating = "NA"
            
            context = {
                "title" : product_title,
                "description" : product_description,
                "features" : featureslist,
                "ratings" : product_rating,
                "images" : product_images,
                "videos" : product_videos
            }

            # Returns the View result to HttpResponse
            html = render_to_string('main-content.html', context)

            response = {
                            'msg':'Product information fetched successfully.', # response message
                            'html': html      
                    }
            return JsonResponse(response, status=200) # return response as JSON
        else:
            response = {
                            'msg':'Internal server error, please try again.', # response message      
                    }
            return JsonResponse(response, status=500) # return response as JSON

