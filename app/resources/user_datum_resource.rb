class UserDatumResource < ApplicationResource
  attribute :id, :integer, writable: false
  attribute :created_at, :datetime, writable: false
  attribute :updated_at, :datetime, writable: false
  attribute :username, :integer
  attribute :password, :integer
  attribute :email_address, :integer

  # Direct associations

  has_many   :user_messagings,
             foreign_key: :recipient_id

  has_many   :seller_id,
             resource: ProductDescriptionResource,
             foreign_key: :seller_id

  # Indirect associations

  has_many :items_for_sales do
    assign_each do |user_datum, items_for_sales|
      items_for_sales.select do |i|
        i.id.in?(user_datum.items_for_sales.map(&:id))
      end
    end
  end

end
