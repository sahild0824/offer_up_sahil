class CreateProductDescriptions < ActiveRecord::Migration[6.0]
  def change
    create_table :product_descriptions do |t|
      t.integer :name_of_item
      t.integer :description
      t.integer :seller_id
      t.integer :sale_address
      t.integer :product_category
      t.integer :product_image
      t.integer :price
      t.integer :sale_status

      t.timestamps
    end
  end
end
