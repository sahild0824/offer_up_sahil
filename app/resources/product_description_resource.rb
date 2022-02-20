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

  has_many   :user_messagings,
             foreign_key: :product_id

  has_many   :items_for_sales,
             foreign_key: :product_id

  belongs_to :seller,
             resource: UserDatumResource

  # Indirect associations
end
