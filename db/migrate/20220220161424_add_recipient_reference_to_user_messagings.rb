class AddRecipientReferenceToUserMessagings < ActiveRecord::Migration[6.0]
  def change
    add_foreign_key :user_messagings, :user_data, column: :recipient_id
    add_index :user_messagings, :recipient_id
    change_column_null :user_messagings, :recipient_id, false
  end
end
