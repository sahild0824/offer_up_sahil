class ProductDescriptionResource < ApplicationResource
  attribute :id, :integer, writable: false
  attribute :created_at, :datetime, writable: false
  attribute :updated_at, :datetime, writable: false
  attribute :name_of_item, :integer
  attribute :description, :integer
  attribute :seller_id, :integer
  attribute :sale_address, :integer
  attribute :product_category, :integer
  attribute :product_image, :integer
  attribute :price, :integer
  attribute :sale_status, :integer

  # Direct associations

  belongs_to :seller,
             resource: UserDatumResource

  # Indirect associations

end
