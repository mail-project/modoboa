<template>
  <v-form ref="vFormRef">
    <label class="m-label">{{ $gettext('Username') }}</label>
    <EmailField
      ref="username"
      v-model="account.username"
      :placeholder="usernamePlaceholder"
      :type="usernameInputType"
      :rules="
        usernameInputType === 'email'
          ? [rules.required, rules.email]
          : [rules.required]
      "
      :role="account.role"
      :error-msg="formErrors.value ? formErrors.value.username : []"
      @update:model-value="updateUsername"
    />
    <label class="m-label">{{ $gettext('First name') }}</label>
    <v-text-field
      v-model="account.first_name"
      autocomplete="new-password"
      variant="outlined"
      density="compact"
    />
    <label class="m-label">{{ $gettext('Last name') }}</label>
    <v-text-field
      v-model="account.last_name"
      autocomplete="new-password"
      variant="outlined"
      density="compact"
    />

    <AccountPasswordSubForm
      v-if="authStore.authUser.pk !== account.pk"
      ref="passwordForm"
      v-model="account"
      :editing="editing"
      :form-errors="formErrors"
    />
    <v-alert v-else type="info" variant="tonal" class="py-2">
      {{ $gettext('You can update your password from the Account section') }}
    </v-alert>

    <v-switch
      v-model="account.is_active"
      :label="$gettext('Enabled')"
      density="compact"
      color="primary"
    />
  </v-form>
</template>

<script setup lang="js">
import AccountPasswordSubForm from './AccountPasswordSubForm.vue'
import EmailField from '@/components/tools/EmailField.vue'
import { ref, computed } from 'vue'
import { useGettext } from 'vue3-gettext'
import { useAuthStore } from '@/stores'
import rules from '@/plugins/rules'
import constants from '@/constants.json'

const { $gettext } = useGettext()
const authStore = useAuthStore()

const props = defineProps({
  modelValue: { type: Object, default: null },
  editing: { type: Boolean, default: false },
})

const vFormRef = ref()
const formErrors = ref({})

const account = computed(() => props.modelValue)

const usernamePlaceholder = computed(() => {
  if (account.value.role === constants.USER) {
    return $gettext('Enter an email address')
  }
  return $gettext('Enter a simple username or an email address')
})

const usernameInputType = computed(() => {
  return account.value.role === constants.USER ? 'email' : 'text'
})

function updateUsername() {
  if (account.value.username.indexOf('@') !== -1) {
    account.value.mailbox.full_address = account.value.username
    account.value.mailbox.message_limit = null
  }
}

defineExpose({ vFormRef, formErrors })
</script>
