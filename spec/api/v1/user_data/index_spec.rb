require "rails_helper"

RSpec.describe "user_data#index", type: :request do
  let(:params) { {} }

  subject(:make_request) do
    jsonapi_get "/api/v1/user_data", params: params
  end

  describe "basic fetch" do
    let!(:user_datum1) { create(:user_datum) }
    let!(:user_datum2) { create(:user_datum) }

    it "works" do
      expect(UserDatumResource).to receive(:all).and_call_original
      make_request
      expect(response.status).to eq(200), response.body
      expect(d.map(&:jsonapi_type).uniq).to match_array(["user_data"])
      expect(d.map(&:id)).to match_array([user_datum1.id, user_datum2.id])
    end
  end
end
