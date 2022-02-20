require "rails_helper"

RSpec.describe "product_descriptions#update", type: :request do
  subject(:make_request) do
    jsonapi_put "/api/v1/product_descriptions/#{product_description.id}",
                payload
  end

  describe "basic update" do
    let!(:product_description) { create(:product_description) }

    let(:payload) do
      {
        data: {
          id: product_description.id.to_s,
          type: "product_descriptions",
          attributes: {
            # ... your attrs here
          },
        },
      }
    end

    # Replace 'xit' with 'it' after adding attributes
    xit "updates the resource" do
      expect(ProductDescriptionResource).to receive(:find).and_call_original
      expect do
        make_request
        expect(response.status).to eq(200), response.body
      end.to change { product_description.reload.attributes }
    end
  end
end
