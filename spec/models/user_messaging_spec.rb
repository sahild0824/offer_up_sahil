require 'rails_helper'

RSpec.describe UserMessaging, type: :model do
  
    describe "Direct Associations" do

    it { should belong_to(:recipient) }

    end

    describe "InDirect Associations" do

    end

    describe "Validations" do

    end
end
