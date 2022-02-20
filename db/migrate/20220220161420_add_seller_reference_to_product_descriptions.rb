class AddSellerReferenceToProductDescriptions < ActiveRecord::Migration[6.0]
  def change
    add_foreign_key :product_descriptions, :user_data, column: :seller_id
    add_index :product_descriptions, :seller_id
    change_column_null :product_descriptions, :seller_id, false
  end
end
