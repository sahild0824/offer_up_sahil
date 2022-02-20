class UserDatumResource < ApplicationResource
  attribute :id, :integer, writable: false
  attribute :created_at, :datetime, writable: false
  attribute :updated_at, :datetime, writable: false
  attribute :username, :integer
  attribute :password, :integer
  attribute :email_address, :integer

  # Direct associations

  has_many   :seller_id,
             resource: ProductDescriptionResource,
             foreign_key: :seller_id

  # Indirect associations

end