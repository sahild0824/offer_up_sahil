json.extract! user_datum, :id, :username, :password, :email_address,
              :created_at, :updated_at
json.url user_datum_url(user_datum, format: :json)
