class CreateUserMessagings < ActiveRecord::Migration[6.0]
  def change
    create_table :user_messagings do |t|
      t.integer :recipient_id
      t.integer :sender_id
      t.integer :message_data
      t.integer :product_id

      t.timestamps
    end
  end
end
