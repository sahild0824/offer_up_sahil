class UserMessagingResource < ApplicationResource
  attribute :id, :integer, writable: false
  attribute :created_at, :datetime, writable: false
  attribute :updated_at, :datetime, writable: false
  attribute :recipient_id, :integer
  attribute :sender_id, :integer
  attribute :message_data, :integer
  attribute :product_id, :integer

  # Direct associations

  # Indirect associations

end
