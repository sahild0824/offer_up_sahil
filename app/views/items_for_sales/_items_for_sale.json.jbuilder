json.extract! items_for_sale, :id, :seller_name, :product_id, :product_description, :price, :product_category, :created_at, :updated_at
json.url items_for_sale_url(items_for_sale, format: :json)
