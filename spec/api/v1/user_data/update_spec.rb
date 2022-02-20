require "rails_helper"

RSpec.describe "user_data#update", type: :request do
  subject(:make_request) do
    jsonapi_put "/api/v1/user_data/#{user_datum.id}", payload
  end

  describe "basic update" do
    let!(:user_datum) { create(:user_datum) }

    let(:payload) do
      {
        data: {
          id: user_datum.id.to_s,
          type: "user_data",
          attributes: {
            # ... your attrs here
          },
        },
      }
    end

    # Replace 'xit' with 'it' after adding attributes
    xit "updates the resource" do
      expect(UserDatumResource).to receive(:find).and_call_original
      expect do
        make_request
        expect(response.status).to eq(200), response.body
      end.to change { user_datum.reload.attributes }
    end
  end
end
