class CreateItemsForSales < ActiveRecord::Migration[6.0]
  def change
    create_table :items_for_sales do |t|
      t.integer :seller_name
      t.integer :product_id
      t.integer :product_description
      t.integer :price
      t.integer :product_category

      t.timestamps
    end
  end
end
