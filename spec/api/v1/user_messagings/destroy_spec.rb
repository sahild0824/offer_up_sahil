require 'rails_helper'

RSpec.describe "user_messagings#destroy", type: :request do
  subject(:make_request) do
    jsonapi_delete "/api/v1/user_messagings/#{user_messaging.id}"
  end

  describe 'basic destroy' do
    let!(:user_messaging) { create(:user_messaging) }

    it 'updates the resource' do
      expect(UserMessagingResource).to receive(:find).and_call_original
      expect {
        make_request
        expect(response.status).to eq(200), response.body
      }.to change { UserMessaging.count }.by(-1)
      expect { user_messaging.reload }
        .to raise_error(ActiveRecord::RecordNotFound)
      expect(json).to eq('meta' => {})
    end
  end
end
