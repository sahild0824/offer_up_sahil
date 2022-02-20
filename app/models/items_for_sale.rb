class ItemsForSale < ApplicationRecord
  # Direct associations

  belongs_to :product,
             :class_name => "ProductDescription"

  # Indirect associations

  # Validations

  # Scopes

  def to_s
    seller_name
  end

end
