class ProductDescription < ApplicationRecord
  # Direct associations

  belongs_to :seller,
             :class_name => "UserDatum"

  # Indirect associations

  # Validations

  # Scopes

  def to_s
    name_of_item
  end

end
