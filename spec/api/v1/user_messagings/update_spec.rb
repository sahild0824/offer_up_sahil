require 'rails_helper'

RSpec.describe "user_messagings#update", type: :request do
  subject(:make_request) do
    jsonapi_put "/api/v1/user_messagings/#{user_messaging.id}", payload
  end

  describe 'basic update' do
    let!(:user_messaging) { create(:user_messaging) }

    let(:payload) do
      {
        data: {
          id: user_messaging.id.to_s,
          type: 'user_messagings',
          attributes: {
            # ... your attrs here
          }
        }
      }
    end

    # Replace 'xit' with 'it' after adding attributes
    xit 'updates the resource' do
      expect(UserMessagingResource).to receive(:find).and_call_original
      expect {
        make_request
        expect(response.status).to eq(200), response.body
      }.to change { user_messaging.reload.attributes }
    end
  end
end
