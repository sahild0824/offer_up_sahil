class ItemsForSale < ApplicationRecord
  # Direct associations

  belongs_to :product,
             class_name: "ProductDescription"

  # Indirect associations

  has_one    :seller,
             through: :product,
             source: :seller

  # Validations

  # Scopes

  def to_s
    seller_name
  end
end
