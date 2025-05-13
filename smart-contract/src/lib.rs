use borsh::{BorshDeserialize, BorshSerialize};
use solana_program::{
    account_info::{next_account_info, AccountInfo},
    entrypoint,
    entrypoint::ProgramResult,
    msg,
    program_error::ProgramError,
    pubkey::Pubkey,
    system_instruction,
    sysvar::{rent::Rent, Sysvar},
    program::{invoke, invoke_signed},
    clock::Clock,
};
use spl_token::{
    instruction as token_instruction,
    state::Account as TokenAccount,
};
use std::convert::TryInto;

#[derive(BorshSerialize, BorshDeserialize, Debug)]
pub struct StakingAccount {
    pub owner: Pubkey,
    pub amount: u64,
    pub start_time: i64,
    pub is_active: bool,
}

#[derive(BorshSerialize, BorshDeserialize, Debug)]
pub enum StakingInstruction {
    Initialize,
    Stake { amount: u64 },
    Unstake,
}

entrypoint!(process_instruction);

pub fn process_instruction(
    program_id: &Pubkey,
    accounts: &[AccountInfo],
    instruction_data: &[u8],
) -> ProgramResult {
    let instruction = StakingInstruction::try_from_slice(instruction_data)?;
    let accounts_iter = &mut accounts.iter();

    match instruction {
        StakingInstruction::Initialize => {
            msg!("Instruction: Initialize");
            process_initialize(program_id, accounts_iter)
        }
        StakingInstruction::Stake { amount } => {
            msg!("Instruction: Stake");
            process_stake(program_id, accounts_iter, amount)
        }
        StakingInstruction::Unstake => {
            msg!("Instruction: Unstake");
            process_unstake(program_id, accounts_iter)
        }
    }
}

fn process_initialize(
    program_id: &Pubkey,
    accounts_iter: &mut std::slice::Iter<AccountInfo>,
) -> ProgramResult {
    let staking_account = next_account_info(accounts_iter)?;
    let owner = next_account_info(accounts_iter)?;
    let system_program = next_account_info(accounts_iter)?;

    if !owner.is_signer {
        return Err(ProgramError::MissingRequiredSignature);
    }

    let rent = Rent::get()?;
    let space = std::mem::size_of::<StakingAccount>();
    let lamports = rent.minimum_balance(space);

    invoke(
        &system_instruction::create_account(
            owner.key,
            staking_account.key,
            lamports,
            space.try_into().unwrap(),
            program_id,
        ),
        &[owner.clone(), staking_account.clone(), system_program.clone()],
    )?;

    let staking_data = StakingAccount {
        owner: *owner.key,
        amount: 0,
        start_time: 0,
        is_active: false,
    };

    staking_data.serialize(&mut *staking_account.data.borrow_mut())?;
    Ok(())
}

fn process_stake(
    program_id: &Pubkey,
    accounts_iter: &mut std::slice::Iter<AccountInfo>,
    amount: u64,
) -> ProgramResult {
    let staking_account = next_account_info(accounts_iter)?;
    let owner = next_account_info(accounts_iter)?;
    let system_program = next_account_info(accounts_iter)?;

    if !owner.is_signer {
        return Err(ProgramError::MissingRequiredSignature);
    }

    let mut staking_data = StakingAccount::try_from_slice(&staking_account.data.borrow())?;
    if staking_data.owner != *owner.key {
        return Err(ProgramError::InvalidAccountData);
    }

    if staking_data.is_active {
        return Err(ProgramError::InvalidAccountData);
    }

    let clock = Clock::get()?;
    staking_data.amount = amount;
    staking_data.start_time = clock.unix_timestamp;
    staking_data.is_active = true;

    staking_data.serialize(&mut *staking_account.data.borrow_mut())?;
    Ok(())
}

fn process_unstake(
    program_id: &Pubkey,
    accounts_iter: &mut std::slice::Iter<AccountInfo>,
) -> ProgramResult {
    let staking_account = next_account_info(accounts_iter)?;
    let owner = next_account_info(accounts_iter)?;
    let system_program = next_account_info(accounts_iter)?;

    if !owner.is_signer {
        return Err(ProgramError::MissingRequiredSignature);
    }

    let mut staking_data = StakingAccount::try_from_slice(&staking_account.data.borrow())?;
    if staking_data.owner != *owner.key {
        return Err(ProgramError::InvalidAccountData);
    }

    if !staking_data.is_active {
        return Err(ProgramError::InvalidAccountData);
    }

    let clock = Clock::get()?;
    let duration = clock.unix_timestamp - staking_data.start_time;
    let days = duration / (24 * 60 * 60);
    let reward_rate = 0.01; // 1% daily reward
    let rewards = (staking_data.amount as f64 * reward_rate * days as f64) as u64;

    // Transfer staked amount + rewards to owner
    let total_amount = staking_data.amount + rewards;
    **staking_account.try_borrow_mut_lamports()? -= total_amount;
    **owner.try_borrow_mut_lamports()? += total_amount;

    staking_data.amount = 0;
    staking_data.start_time = 0;
    staking_data.is_active = false;

    staking_data.serialize(&mut *staking_account.data.borrow_mut())?;
    Ok(())
} 