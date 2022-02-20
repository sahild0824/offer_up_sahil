class UserDatum < ApplicationRecord
  # Direct associations

  has_many   :seller_id,
             :class_name => "ProductDescription",
             :foreign_key => "seller_id",
             :dependent => :destroy

  # Indirect associations

  # Validations

  # Scopes

  def to_s
    username
  end

end
