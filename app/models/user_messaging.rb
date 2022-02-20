class UserMessaging < ApplicationRecord
  # Direct associations

  belongs_to :product,
             :class_name => "ProductDescription"

  belongs_to :recipient,
             :class_name => "UserDatum"

  # Indirect associations

  # Validations

  # Scopes

  def to_s
    recipient.to_s
  end

end
