class UserMessaging < ApplicationRecord
  # Direct associations

  # Indirect associations

  # Validations

  # Scopes

  def to_s
    recipient.to_s
  end

end
