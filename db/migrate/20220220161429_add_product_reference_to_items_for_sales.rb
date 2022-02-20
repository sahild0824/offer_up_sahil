class AddProductReferenceToItemsForSales < ActiveRecord::Migration[6.0]
  def change
    add_foreign_key :items_for_sales, :product_descriptions, column: :product_id
    add_index :items_for_sales, :product_id
    change_column_null :items_for_sales, :product_id, false
  end
end
