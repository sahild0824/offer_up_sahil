class UserDatum < ApplicationRecord
  # Direct associations

  has_many   :user_messagings,
             foreign_key: "recipient_id",
             dependent: :destroy

  has_many   :seller_id,
             class_name: "ProductDescription",
             foreign_key: "seller_id",
             dependent: :destroy

  # Indirect associations

  has_many   :items_for_sales,
             through: :seller_id,
             source: :items_for_sales

  # Validations

  # Scopes

  def to_s
    username
  end
end
