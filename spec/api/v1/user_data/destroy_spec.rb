require 'rails_helper'

RSpec.describe "user_data#destroy", type: :request do
  subject(:make_request) do
    jsonapi_delete "/api/v1/user_data/#{user_datum.id}"
  end

  describe 'basic destroy' do
    let!(:user_datum) { create(:user_datum) }

    it 'updates the resource' do
      expect(UserDatumResource).to receive(:find).and_call_original
      expect {
        make_request
        expect(response.status).to eq(200), response.body
      }.to change { UserDatum.count }.by(-1)
      expect { user_datum.reload }
        .to raise_error(ActiveRecord::RecordNotFound)
      expect(json).to eq('meta' => {})
    end
  end
end
