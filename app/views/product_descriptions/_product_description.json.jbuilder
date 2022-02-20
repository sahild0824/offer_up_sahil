json.extract! product_description, :id, :name_of_item, :description,
              :seller_id, :sale_address, :product_category, :product_image, :price, :sale_status, :created_at, :updated_at
json.url product_description_url(product_description, format: :json)
