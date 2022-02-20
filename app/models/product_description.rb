class ProductDescription < ApplicationRecord
  # Direct associations

  has_many   :user_messagings,
             :foreign_key => "product_id",
             :dependent => :destroy

  has_many   :items_for_sales,
             :foreign_key => "product_id",
             :dependent => :destroy

  belongs_to :seller,
             :class_name => "UserDatum"

  # Indirect associations

  # Validations

  # Scopes

  def to_s
    name_of_item
  end

end
