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

  has_one    :seller,
             resource: UserDatumResource

  filter :seller_id, :integer do
    eq do |scope, value|
      scope.eager_load(:seller).where(product_descriptions: { seller_id: value })
    end
  end
end
