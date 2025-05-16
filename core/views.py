from django.shortcuts import render
import os
from dotenv import load_dotenv
import shopify
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import requests

load_dotenv()

def shopify_test(request):
    shop_url = os.getenv("SHOPIFY_SHOP_URL")
    access_token = os.getenv("SHOPIFY_API_TOKEN")
    api_version = os.getenv("SHOPIFY_API_VERSION", "2025-04")

    session = shopify.Session(shop_url, version=api_version, token=access_token)
    shopify.ShopifyResource.activate_session(session)

    shop = shopify.Shop.current()
    return JsonResponse(shop.to_dict())

@csrf_exempt
def order_updated_webhook(request):
    if request.method == "POST":
        data = json.loads(request.body)

        order_number = data.get("name")  
        customer = data.get("customer", {})
        customer_name = f"{customer.get('first_name', '')} {customer.get('last_name', '')}".strip()

        print(f"[Webhook] Order edited: {order_number} | Customer: {customer_name}")
        print(f"[Webhook] Webhook data: {data}")

        return HttpResponse(status=200)
    return HttpResponse(status=405)

def register_webhook(request):
    shop_url = os.getenv("SHOPIFY_SHOP_URL")
    access_token = os.getenv("SHOPIFY_API_TOKEN")

    webhook_url = os.getenv("WEBHOOK_URL")

    headers = {
        "Content-Type": "application/json",
        "X-Shopify-Access-Token": access_token
    }

    payload = {
        "webhook": {
            "topic": "orders/updated",
            "address": webhook_url,
            "format": "json"
        }
    }

    response = requests.post(
        f"https://{shop_url}/admin/api/2024-04/webhooks.json",
        headers=headers,
        json=payload
    )

    return JsonResponse(response.json(), status=response.status_code)