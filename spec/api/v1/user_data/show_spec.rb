require 'rails_helper'

RSpec.describe "user_data#show", type: :request do
  let(:params) { {} }

  subject(:make_request) do
    jsonapi_get "/api/v1/user_data/#{user_datum.id}", params: params
  end

  describe 'basic fetch' do
    let!(:user_datum) { create(:user_datum) }

    it 'works' do
      expect(UserDatumResource).to receive(:find).and_call_original
      make_request
      expect(response.status).to eq(200)
      expect(d.jsonapi_type).to eq('user_data')
      expect(d.id).to eq(user_datum.id)
    end
  end
end
