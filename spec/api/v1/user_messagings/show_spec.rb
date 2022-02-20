require 'rails_helper'

RSpec.describe "user_messagings#show", type: :request do
  let(:params) { {} }

  subject(:make_request) do
    jsonapi_get "/api/v1/user_messagings/#{user_messaging.id}", params: params
  end

  describe 'basic fetch' do
    let!(:user_messaging) { create(:user_messaging) }

    it 'works' do
      expect(UserMessagingResource).to receive(:find).and_call_original
      make_request
      expect(response.status).to eq(200)
      expect(d.jsonapi_type).to eq('user_messagings')
      expect(d.id).to eq(user_messaging.id)
    end
  end
end
