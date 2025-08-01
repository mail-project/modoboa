<template>
  <LoadingData v-if="working" />
  <div v-else>
    <v-expansion-panels v-model="panel" :multiple="formErrors">
      <v-expansion-panel v-if="canSetRole" eager value="roleForm">
        <v-expansion-panel-title v-slot="{ expanded }">
          <v-row no-gutters>
            <v-col cols="4">
              {{ $gettext('Role') }}
            </v-col>
            <v-col cols="8" class="text-medium-emphasis">
              <v-fade-transition leave-absolute>
                <span v-if="expanded"></span>
                <v-row v-else no-gutters style="width: 100%">
                  <v-col v-if="roleForm" cols="6">
                    {{ roleForm.roleLabel }}
                  </v-col>
                </v-row>
              </v-fade-transition>
            </v-col>
          </v-row>
        </v-expansion-panel-title>
        <v-expansion-panel-text>
          <AccountRoleForm ref="roleForm" v-model="editedAccount" />
        </v-expansion-panel-text>
      </v-expansion-panel>
      <v-expansion-panel eager value="generalForm">
        <v-expansion-panel-title v-slot="{ expanded }">
          <v-row no-gutters>
            <v-col cols="4">
              {{ $gettext('Identification') }}
            </v-col>
            <v-col cols="8" class="">
              <v-fade-transition leave-absolute>
                <span v-if="expanded"></span>
                <v-row v-else no-gutters style="width: 100%">
                  <v-col cols="6">
                    <div class="mr-2">
                      {{ $gettext('Username:') }}
                      {{ editedAccount.username }}
                    </div>
                  </v-col>
                  <v-col cols="6">
                    <div class="mr-2">
                      {{ $gettext('Enabled') }}
                      <v-icon v-if="editedAccount.is_active" color="success"
                        >mdi-check-circle-outline</v-icon
                      >
                      <v-icon v-else>mdi-close-circle-outline</v-icon>
                    </div>
                  </v-col>
                </v-row>
              </v-fade-transition>
            </v-col>
          </v-row>
        </v-expansion-panel-title>
        <v-expansion-panel-text>
          <AccountGeneralForm
            ref="generalForm"
            v-model="editedAccount"
            editing
          />
        </v-expansion-panel-text>
      </v-expansion-panel>
      <v-expansion-panel v-if="usernameIsEmail" eager value="mailboxForm">
        <v-expansion-panel-title v-slot="{ expanded }">
          <v-row no-gutters>
            <v-col cols="4">
              {{ $gettext('Mailbox') }}
            </v-col>
            <v-col cols="8" class="">
              <v-fade-transition leave-absolute>
                <span v-if="expanded"></span>
                <v-row v-else no-gutters style="width: 100%">
                  <template v-if="editedAccount.mailbox">
                    <v-col
                      v-if="editedAccount.mailbox.use_domain_quota"
                      cols="6"
                    >
                      <div class="mr-2">
                        {{ $gettext('Quota: ') }}
                        {{ $gettext("domain's default value") }}
                      </div>
                    </v-col>
                    <v-col v-else cols="6">
                      <div class="mr-2">
                        {{ $gettext('Quota: ') }}
                        {{ editedAccount.mailbox.quota }}
                      </div>
                    </v-col>
                    <v-col cols="6">
                      <div class="mr-2">
                        {{ $gettext('Send only') }}
                        <v-icon
                          v-if="editedAccount.mailbox.is_send_only"
                          color="success"
                          >mdi-check-circle-outline</v-icon
                        >
                        <v-icon v-else>mdi-close-circle-outline</v-icon>
                      </div>
                    </v-col>
                  </template>
                </v-row>
              </v-fade-transition>
            </v-col>
          </v-row>
        </v-expansion-panel-title>
        <v-expansion-panel-text>
          <AccountMailboxForm ref="mailboxForm" v-model="editedAccount" />
        </v-expansion-panel-text>
      </v-expansion-panel>
      <v-expansion-panel v-if="usernameIsEmail" eager value="aliasForm">
        <v-expansion-panel-title v-slot="{ expanded }">
          <v-row no-gutters>
            <v-col cols="4">
              {{ $gettext('Alias') }}
            </v-col>
            <v-col cols="8" class="">
              <v-fade-transition leave-absolute>
                <span v-if="expanded"></span>
                <v-row v-else no-gutters style="width: 100%">
                  <template v-if="editedAccount.aliases">
                    <v-col cols="6">
                      <div class="mr-2">
                        {{ $gettext('Number of associated alias:') }}
                        {{ editedAccount.aliases.length }}
                      </div>
                    </v-col>
                  </template>
                </v-row>
              </v-fade-transition>
            </v-col>
          </v-row>
        </v-expansion-panel-title>
        <v-expansion-panel-text>
          <AccountAliasForm ref="aliasForm" v-model="editedAccount" />
        </v-expansion-panel-text>
      </v-expansion-panel>
      <v-expansion-panel v-if="needsResources" eager value="resourcesForm">
        <v-expansion-panel-title v-slot="{ expanded }">
          <v-row no-gutters>
            <v-col cols="4">
              {{ $gettext('Resources') }}
            </v-col>
            <v-col cols="8" class="">
              <v-fade-transition leave-absolute>
                <span v-if="expanded"></span>
                <v-row v-else no-gutters style="width: 100%">
                  <template
                    v-if="
                      editedAccount.resources != undefined &&
                      editedAccount.resources.length == 2
                    "
                  >
                    <v-col cols="6">
                      <div class="mr-2">
                        {{ $gettext('Number of allowed mailboxes:') }}
                        {{ editedAccount.resources[0].max_value }}
                      </div>
                    </v-col>
                    <v-col cols="6">
                      <div class="mr-2">
                        {{ $gettext('Number of allowed mailbox aliases:') }}
                        {{ editedAccount.resources[1].max_value }}
                      </div>
                    </v-col>
                  </template>
                </v-row>
              </v-fade-transition>
            </v-col>
          </v-row>
        </v-expansion-panel-title>
        <v-expansion-panel-text>
          <ResourcesForm
            ref="resourcesForm"
            v-model="editedAccount.resources"
          />
        </v-expansion-panel-text>
      </v-expansion-panel>
    </v-expansion-panels>
    <div class="mt-4 d-flex justify-end">
      <v-btn :loading="working" variant="outlined" @click="$router.go(-1)">
        {{ $gettext('Cancel') }}
      </v-btn>
      <v-btn
        class="ml-4"
        color="primary darken-1"
        variant="outlined"
        :loading="working"
        @click="save"
      >
        {{ $gettext('Save') }}
      </v-btn>
    </div>
  </div>
</template>

<script setup lang="js">
import { useAuthStore } from '@/stores'
import AccountGeneralForm from './form_steps/AccountGeneralForm.vue'
import AccountMailboxForm from './form_steps/AccountMailboxForm.vue'
import AccountAliasForm from './form_steps/AccountAliasForm.vue'
import AccountRoleForm from './form_steps/AccountRoleForm.vue'
import ResourcesForm from '@/components/tools/ResourcesForm.vue'
import LoadingData from '@/components/tools/LoadingData.vue'
import accountsApi from '@/api/accounts.js'
import parametersApi from '@/api/parameters'
import { ref, computed, onMounted, watch } from 'vue'
import { useGettext } from 'vue3-gettext'
import { useRoute, useRouter } from 'vue-router'
import { usePermissions } from '@/composables/permissions'
import constants from '@/constants.json'

const { $gettext } = useGettext()
const authStore = useAuthStore()
const route = useRoute()
const router = useRouter()
const { canSetRole } = usePermissions()

const editedAccount = ref({ pk: route.params.id })

const usernameIsEmail = computed(() => {
  return (
    editedAccount.value.username &&
    editedAccount.value.username.indexOf('@') !== -1
  )
})

const needsResources = computed(() => {
  const isNeeded =
    limitsConfig.value.params &&
    limitsConfig.value.params.enable_admin_limits &&
    editedAccount.value.role !== constants.USER &&
    editedAccount.value.role !== constants.SUPER_ADMIN
  if (isNeeded === undefined) {
    return false
  }
  return isNeeded
})

const limitsConfig = ref({})
const panel = ref(0)
const working = ref(false)
const formErrors = ref(false)

//refs
const roleForm = ref()
const generalForm = ref()
const mailboxForm = ref()
const aliasForm = ref()
const resourcesForm = ref()

//formMap
const formMap = computed(() => {
  const map = {
    roleForm: roleForm,
    generalForm: generalForm,
  }
  if (usernameIsEmail.value) {
    map.aliasForm = aliasForm
    map.mailboxForm = mailboxForm
  }
  if (needsResources.value) {
    map.resourcesForm = resourcesForm
  }
  return map
})

async function save() {
  formErrors.value = false
  panel.value = []
  for (const [panelName, formRef] of Object.entries(formMap.value)) {
    if (formRef.value != null) {
      const { valid } = await formRef.value.vFormRef.validate()
      if (!valid) {
        formErrors.value = true
        panel.value.push(panelName)
      }
    }
  }
  if (formErrors.value) {
    return
  }
  working.value = true
  try {
    const data = { ...editedAccount.value }
    if (usernameIsEmail.value) {
      data.mailbox.full_address = data.username
    } else if (data.mailbox) {
      delete data.mailbox.full_address
    }
    if (data.new_password) {
      data.password = data.new_password
      delete data.new_password
      delete data.password_confirmation
    }
    if (needsResources.value && resourcesForm.value !== null) {
      data.resources = resourcesForm.value.getPayload()
    }
    if (data.aliases === null) {
      delete data.aliases
    }
    if (!canSetRole.value) {
      if (editedAccount.value.pk === authStore.authUser.pk) {
        data.role = authStore.authUser.role
      } else {
        data.role = constants.USER
      }
    }
    await accountsApi.patch(editedAccount.value.pk, data)
    router.push({
      name: 'AccountDetail',
      params: { id: route.params.id },
    })
  } finally {
    working.value = false
  }
}

onMounted(() => {
  accountsApi.get(route.params.id).then((response) => {
    editedAccount.value = response.data
    working.value = false
  })

  if (canSetRole.value) {
    parametersApi.getGlobalApplication('limits').then((response) => {
      limitsConfig.value = response.data
    })
  }
})

watch(
  editedAccount,
  () => {
    delete editedAccount.value.domains
    if (editedAccount.value.mailbox === null) {
      delete editedAccount.value.mailbox
    }
  },
  { deep: true }
)
</script>
