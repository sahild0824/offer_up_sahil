class AddProductReferenceToUserMessagings < ActiveRecord::Migration[6.0]
  def change
    add_foreign_key :user_messagings, :product_descriptions, column: :product_id
    add_index :user_messagings, :product_id
    change_column_null :user_messagings, :product_id, false
  end
end
