class ItemsForSaleResource < ApplicationResource
  attribute :id, :integer, writable: false
  attribute :created_at, :datetime, writable: false
  attribute :updated_at, :datetime, writable: false
  attribute :seller_name, :integer
  attribute :product_id, :integer
  attribute :product_description, :integer
  attribute :price, :integer
  attribute :product_category, :integer

  # Direct associations

  belongs_to :product,
             resource: ProductDescriptionResource

  # Indirect associations

end
