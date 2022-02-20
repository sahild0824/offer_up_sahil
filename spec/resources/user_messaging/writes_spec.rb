require "rails_helper"

RSpec.describe UserMessagingResource, type: :resource do
  describe "creating" do
    let(:payload) do
      {
        data: {
          type: "user_messagings",
          attributes: {},
        },
      }
    end

    let(:instance) do
      UserMessagingResource.build(payload)
    end

    it "works" do
      expect do
        expect(instance.save).to eq(true),
                                 instance.errors.full_messages.to_sentence
      end.to change { UserMessaging.count }.by(1)
    end
  end

  describe "updating" do
    let!(:user_messaging) { create(:user_messaging) }

    let(:payload) do
      {
        data: {
          id: user_messaging.id.to_s,
          type: "user_messagings",
          attributes: {}, # Todo!
        },
      }
    end

    let(:instance) do
      UserMessagingResource.find(payload)
    end

    xit "works (add some attributes and enable this spec)" do
      expect do
        expect(instance.update_attributes).to eq(true)
      end.to change { user_messaging.reload.updated_at }
      # .and change { user_messaging.foo }.to('bar') <- example
    end
  end

  describe "destroying" do
    let!(:user_messaging) { create(:user_messaging) }

    let(:instance) do
      UserMessagingResource.find(id: user_messaging.id)
    end

    it "works" do
      expect do
        expect(instance.destroy).to eq(true)
      end.to change { UserMessaging.count }.by(-1)
    end
  end
end
