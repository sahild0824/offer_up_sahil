class CreateUserData < ActiveRecord::Migration[6.0]
  def change
    create_table :user_data do |t|
      t.integer :username
      t.integer :password
      t.integer :email_address

      t.timestamps
    end
  end
end
