require "rails_helper"

RSpec.describe "user_messagings#index", type: :request do
  let(:params) { {} }

  subject(:make_request) do
    jsonapi_get "/api/v1/user_messagings", params: params
  end

  describe "basic fetch" do
    let!(:user_messaging1) { create(:user_messaging) }
    let!(:user_messaging2) { create(:user_messaging) }

    it "works" do
      expect(UserMessagingResource).to receive(:all).and_call_original
      make_request
      expect(response.status).to eq(200), response.body
      expect(d.map(&:jsonapi_type).uniq).to match_array(["user_messagings"])
      expect(d.map(&:id)).to match_array([user_messaging1.id,
                                          user_messaging2.id])
    end
  end
end
