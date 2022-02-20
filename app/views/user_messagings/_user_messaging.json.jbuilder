json.extract! user_messaging, :id, :recipient_id, :sender_id, :message_data, :product_id, :created_at, :updated_at
json.url user_messaging_url(user_messaging, format: :json)
